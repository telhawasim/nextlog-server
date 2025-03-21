//
//  EmployeeController.swift
//  Nextlog-server
//
//  Created by Telha Wasim on 18/03/2025.
//

import Vapor
import Fluent
@preconcurrency import FluentMongoDriver
import JWT

struct EmployeeController: RouteCollection {
    
    //MARK: - BOOT -
    func boot(routes: any RoutesBuilder) throws {
        let employee = routes.grouped("employee")
        let protected = employee.grouped(JWTMiddleware())
        /// Without JWT
        employee.post("login", use: self.loginAsEmployee)
        /// With JWT
        protected.post("add", use: self.addEmployee)
        protected.get("detail", ":id", use: self.getSpecificEmployee)
        protected.delete("delete", use: self.deleteEmployee)
        protected.get("getAll", use: self.getAllEmployees)
    }
}

//MARK: - FUNCTIONS -
extension EmployeeController {
    
    //MARK: - ADD EMPLOYEE -
    @Sendable private func addEmployee(req: Request) async throws -> BaseServer {
        /// Decode the request
        let formData = try req.content.decode(AddEmployeeRequest.self)
        /// Validate the request
        try formData.validate()
        /// Check designation exists in the database
        guard let existingDesignation = try await DesignationModel.query(on: req.db)
            .filter(\.$id == formData.designation_id ?? ObjectId())
            .first()
        else {
            return BaseServer(message: "Designation does not exist", status: .badRequest)
        }
        /// Check department exists in the database
        guard let existingDepartment = try await DepartmentModel.query(on: req.db)
            .filter(\.$id == formData.department_id ?? ObjectId())
            .first()
        else {
            return BaseServer(message: "Department does not exist", status: .badRequest)
        }
        /// Save the data locally and store the image path in database
        let imagePath = try await saveImageFile(image: formData.avatar, req: req)
        /// Employee model which needs to be saved in database
        let employee = EmployeeModel(
            id: ObjectId(),
            name: formData.name ?? "",
            email: formData.email ?? "",
            emp_id: formData.emp_id ?? 0,
            avatar: imagePath,
            designation: existingDesignation.id ?? ObjectId(),
            department: existingDepartment.id ?? ObjectId(),
            dob: formData.dob ?? Date(),
            phone: formData.phone ?? "",
            date_of_joining: formData.date_of_joining ?? Date()
        )
        /// Save model in database
        try await employee.save(on: req.db)
        /// Return
        return BaseServer(message: "Employee has been added", status: .ok)
    }
    
    //MARK: - GET ALL EMPLOYEES -
    @Sendable private func getAllEmployees(req: Request) async throws -> GetAllEmployeeResponse {
        /// Extract query parameters (optional)
        let page: Int = req.query[Int.self, at: "page"] ?? 1  // Default to page 1
        let limit: Int = req.query[Int.self, at: "limit"] ?? 10 // Default limit 10
        
        /// Validate input (ensure page and limit are positive numbers)
        guard page > 0, limit > 0 else {
            throw Abort(.badRequest, reason: "Page and limit must be positive numbers")
        }
        
        /// Extract total employee count
        let totalEmployees = try await EmployeeModel.query(on: req.db).count()
        
        /// Fetch employees with pagination
        let employees = try await EmployeeModel.query(on: req.db)
            .with(\.$designation)
            .with(\.$department)
            .with(\.$profiles)
            .range((page - 1) * limit..<(page * limit)) // Pagination logic
            .all()
        
        /// Construct response model
        let response = employees.map { employee in
            let avatarPath = employee.avatar.trimmingCharacters(in: CharacterSet(charactersIn: "/"))
            let avatarURL = "http://127.0.0.1:8080/\(avatarPath)"
            
            return EmployeeListRowResponse(
                id: employee.id,
                name: employee.name,
                designation: employee.designation,
                email: employee.email,
                avatar: avatarURL
            )
        }
        /// Response
        return GetAllEmployeeResponse(
            message: "Success",
            status: .ok,
            employees: response,
            current_page: page,
            per_page: limit,
            total: totalEmployees,
            total_pages: Int(ceil(Double(totalEmployees) / Double(limit)))
        )
    }
    
    //MARK: - GET SPECIFIC EMPLOYEE -
    @Sendable private func getSpecificEmployee(req: Request) async throws -> GetSpecificEmploeeResponse {
        /// Decode the request to get the employee ID
        guard let employeeID = req.parameters.get("id"), let objectID = ObjectId(employeeID) else {
            throw Abort(.badRequest, reason: "Invalid employee ID")
        }
        /// Extract the employee from the database
        guard let employee = try await EmployeeModel.query(on: req.db)
            .filter(\.$id == objectID)
            .with(\.$designation)
            .with(\.$department)
            .first() else {
            throw Abort(.notFound, reason: "Employee not found")
        }
        /// Handle the URL for the image
        let avatarPath = employee.avatar.trimmingCharacters(in: CharacterSet(charactersIn: "/"))
        let avatarURL = "http://127.0.0.1:8080/\(avatarPath)"
        /// Return the employee object
        return GetSpecificEmploeeResponse(
            message: "Success",
            status: .ok,
            employee: EmployeeResponse(
                name: employee.name,
                email: employee.email,
                id: employee.id,
                designation: employee.designation,
                department: employee.department,
                avatar: avatarURL,
                created_at: employee.created_at,
                updated_at: employee.updated_at,
                emp_id: employee.emp_id,
                dob: employee.dob,
                date_of_joining: employee.date_of_joining,
                phone: employee.phone
            )
        )
    }
    
    //MARK: - DELETE EMPLOYEE -
    @Sendable private func deleteEmployee(req: Request) async throws -> BaseServer {
        /// Decode the request
        let deleteEmployeeRequest = try req.content.decode(DeleteEmployeeRequest.self)
        /// Validate the request
        try deleteEmployeeRequest.validate()
        /// Extract the user with the same id as request
        guard let existingEmployee = try await EmployeeModel.query(on: req.db)
            .filter(\.$id == deleteEmployeeRequest.id ?? ObjectId())
            .with(\.$profiles)
            .first()
        else {
            return BaseServer(message: "Employee doesn't exist", status: .badRequest)
        }
        /// Delete the associated profiles with the employee
        try await existingEmployee.$profiles.query(on: req.db)
            .delete()
        /// Make the avatar path
        let filePath = req.application.directory.publicDirectory + existingEmployee.avatar
        let fileManager = FileManager.default
        /// Check whether image exists
        if fileManager.fileExists(atPath: filePath) {
            do {
                try fileManager.removeItem(atPath: filePath)
                req.logger.info("Deleted avatar file: \(filePath)")
            } catch {
                req.logger.error("Failed to delete avatar file: \(error.localizedDescription)")
            }
        }
        /// Delete the user from the database
        try await existingEmployee.delete(on: req.db)
        /// Return
        return BaseServer(message: "Employee has been deleted", status: .ok)
    }
    
    //MARK: - LOGIN AS EMPLOYEE -
    @Sendable private func loginAsEmployee(req: Request) async throws -> LoginEmployeeResponse {
        /// Decode the request
        let loginEmployeeRequest = try req.content.decode(LoginEmployeeRequest.self)
        /// Validate the request
        try loginEmployeeRequest.validate()
        /// Extract the existing employee
        guard let existingEmployee = try await EmployeeModel.query(on: req.db)
            .filter(\.$email == loginEmployeeRequest.email ?? "")
            .filter(\.$emp_id == loginEmployeeRequest.id ?? 0)
            .first()
        else {
            throw Abort(.notFound, reason: "Employee not found")
        }
        /// Generate JWT Token
        let payload = JWTTokenPayload(
            id: existingEmployee.id ?? ObjectId(),
            isAdmin: true,
            exp: ExpirationClaim(value: Date().addingTimeInterval(3600)) // 1 hour
        )
        /// Token into string
        let token = try await req.jwt.sign(payload)
        /// Return the response
        return LoginEmployeeResponse(
            message: "Success",
            status: .ok,
            access_token: token,
            data: LoginEmployee(
                id: existingEmployee.id,
                name: existingEmployee.name,
                role: existingEmployee.role
            )
        )
    }
    
    //MARK: - SAVE IMAGE FILE -
    private func saveImageFile(image: File?, req: Request) async throws -> String {
        guard let image = image else {
            return ""
        }
        let fileExtension = image.filename.split(separator: ".").last.map { ".\($0)" } ?? ".jpg"
        let fileName = UUID().uuidString + fileExtension
        let uploadDirectory = req.application.directory.publicDirectory + "uploads/"
        let filePath = uploadDirectory + fileName

        // Ensure directory exists
        try FileManager.default.createDirectory(atPath: uploadDirectory, withIntermediateDirectories: true)

        // Convert ByteBuffer to Data
        var buffer = image.data
        let imageData = buffer.readData(length: buffer.readableBytes) ?? Data()

        // Save the file
        try imageData.write(to: URL(fileURLWithPath: filePath))

        return "uploads/\(fileName)"
    }
    
//    //MARK: - LOGIN AS EMPLOYEE -
//    @Sendable private func loginAsEmployee(req: Request) async throws -> LoginEmployeeResponse {
//        /// Decode the request
//        let loginRequest = try req.content.decode(LoginEmployeeRequest.self)
//        /// Validate the request
//        try loginRequest.validate()
//        /// Extract the existing employee from the database
//        guard let existingEmployee = try await EmployeeModel.query(on: req.db)
//            .filter(\.$email == loginRequest.email ?? "")
//            .filter(\.$emp_id == loginRequest.id ?? 0)
//            .with(\.$designation)
//            .with(\.$department)
//            .with(\.$profiles)
//            .first()
//        else {
//            throw Abort(.badRequest, reason: "Employee not found")
//        }
//        /// Generate JWT Token
//        let payload = JWTTokenPayload(
//            id: existingEmployee.id ?? ObjectId(),
//            isAdmin: true,
//            exp: ExpirationClaim(value: Date().addingTimeInterval(3600)) // 1 hour
//        )
//        /// Token into string
//        let token = try await req.jwt.sign(payload)
//        /// Extract the profile associated with the existing employee
//        let profiles = existingEmployee.profiles.map { profile in
//            GetProfileResponse(id: profile.id, name: profile.name)
//        }
//        /// Handle the URL for the image
//        let avatarPath = existingEmployee.avatar.trimmingCharacters(in: CharacterSet(charactersIn: "/"))
//        let avatarURL = "http://127.0.0.1:8080/\(avatarPath)"
//        /// Return the response
//        return LoginEmployeeResponse(
//            message: "Success",
//            status: .ok,
//            access_token: token,
//            data: EmployeeResponse(
//                name: existingEmployee.name,
//                email: existingEmployee.email,
//                id: existingEmployee.id,
//                designation: existingEmployee.designation,
//                department: existingEmployee.department,
//                avatar: avatarURL,
//                created_at: existingEmployee.created_at,
//                updated_at: existingEmployee.updated_at,
//                emp_id: existingEmployee.emp_id,
//                dob: existingEmployee.dob,
//                date_of_joining: existingEmployee.date_of_joining,
//                phone: existingEmployee.phone,
//                profiles: profiles
//            )
//        )
//    }
}
