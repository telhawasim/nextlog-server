//
//  DepartmentController.swift
//  Nextlog-server
//
//  Created by Telha Wasim on 18/03/2025.
//

import Vapor
import Fluent
import FluentMongoDriver

struct DepartmentController: RouteCollection {
    
    //MARK: - BOOT -
    func boot(routes: any RoutesBuilder) throws {
        let designation = routes.grouped("department")

        designation.post("add", use: self.addDepartment)
        designation.get("getAll", use: self.getAllDepartments)
    }
}

//MARK: - FUNCTIONS -
extension DepartmentController {
    
    //MARK: - ADD DEPARTMENT -
    @Sendable private func addDepartment(req: Request) async throws -> BaseServer {
        /// Decode the request parameters
        let addDepartmentRequest = try req.content.decode(AddDepartmentRequest.self)
        /// Validate the request
        try addDepartmentRequest.validate()
        /// Extract the object where department is already exst in database
        let existingDepartment = try await DepartmentModel.query(on: req.db)
            .filter(\.$name == addDepartmentRequest.name ?? "")
            .first()
        /// Check if department already exists
        if (existingDepartment != nil) {
            throw Abort(.badRequest, reason: "Desigantion already exist")
        }
        /// Make an object which needs to be saved in database
        let department = DepartmentModel(
            id: ObjectId(),
            name: addDepartmentRequest.name ?? ""
        )
        /// Save in the database
        try await department.save(on: req.db)
        /// Return
        return BaseServer(message: "Department added successfully", status: .ok)
    }
    
    //MARK: - GET ALL DEPARTMENTS -
    @Sendable private func getAllDepartments(req: Request) async throws -> GetAllDepartmentsResponse {
        /// Extract the designations from the database
        let departments = try await DepartmentModel.query(on: req.db)
            .all()
        /// Return
        return GetAllDepartmentsResponse(message: "Success", status: .ok, departments: departments)
    }
}
