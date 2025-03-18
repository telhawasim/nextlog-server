//
//  EmployeeController.swift
//  Nextlog-server
//
//  Created by Telha Wasim on 18/03/2025.
//

import Vapor
import Fluent
@preconcurrency import FluentMongoDriver

struct EmployeeController: RouteCollection {
    
    //MARK: - BOOT -
    func boot(routes: any RoutesBuilder) throws {
        let employee = routes.grouped("employee")

        employee.post("add", use: self.addEmployee)
        employee.get("getAll", use: self.getAllEmployees)
        employee.delete("delete", use: self.deleteEmployee)
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
        guard let _ = try await DesignationModel.query(on: req.db)
            .filter(\.$id == formData.designation_id ?? ObjectId())
            .first()
        else {
            return BaseServer(message: "Designation does not exist", status: .badRequest)
        }
        /// Check department exists in the database
        guard let _ = try await DepartmentModel.query(on: req.db)
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
            avatar: imagePath,
            designation: formData.designation_id ?? ObjectId(),
            department: formData.department_id ?? ObjectId()
        )
        /// Save model in database
        try await employee.save(on: req.db)
        /// Return
        return BaseServer(message: "Employee has been added", status: .ok)
    }
    
    //MARK: - GET ALL EMPLOYEES -
    @Sendable private func getAllEmployees(req: Request) async throws -> GetAllEmployeeResponse {
        let employees = try await EmployeeModel.query(on: req.db)
            .with(\.$designation)
            .with(\.$department)
            .all()
        
        let response = employees.map { employee in
            let avatarPath = employee.avatar.trimmingCharacters(in: CharacterSet(charactersIn: "/"))
            let avatarURL = "http://127.0.0.1:8080/\(avatarPath)"

            return EmployeeResponse(
                name: employee.name,
                email: employee.email,
                id: employee.id,
                designation: employee.designation,
                department: employee.department,
                avatarURL: avatarPath.isEmpty ? nil : avatarURL
            )
        }
        
        return GetAllEmployeeResponse(message: "Success", status: .ok, employees: response)
    }
    
    //MARK: - DELETE EMPLOYEE -
    @Sendable private func deleteEmployee(req: Request) async throws -> BaseServer {
        /// Decode the request
        let deleteEmployeeRequest = try req.content.decode(DeleteEmployeeRequest.self)
        /// Extract the user with the same id as request
        let existingEmployee = try await EmployeeModel.query(on: req.db)
            .filter(\.$id == deleteEmployeeRequest.id ?? ObjectId())
            .first()
        /// Check if there is no existing user for the provided id
        if (existingEmployee == nil) {
            return BaseServer(message: "Employee doesn't exist", status: .badRequest)
        }
        /// Delete the user from the database
        try await existingEmployee?.delete(on: req.db)
        /// Return
        return BaseServer(message: "Employee has been deleted", status: .ok)
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
}
