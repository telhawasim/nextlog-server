//
//  ProfileController.swift
//  Nextlog-server
//
//  Created by Telha Wasim on 19/03/2025.
//

import Vapor
import Fluent
@preconcurrency import FluentMongoDriver

struct ProfileController: RouteCollection {
    
    //MARK: - BOOT -
    func boot(routes: any RoutesBuilder) throws {
        let profile = routes.grouped("profile")
        let protected = profile.grouped(JWTMiddleware())

        protected.post("create", use: self.createProfile)
    }
    
    //MARK: - CREATE PROFILE -
    @Sendable private func createProfile(req: Request) async throws -> BaseServer {
        /// Decode the request
        let createProfileRequest = try req.content.decode(CreateProfileRequest.self)
        /// Extract the existing employee
        guard let existingEmployee = try await EmployeeModel.find(createProfileRequest.employee_id ?? ObjectId(), on: req.db) else {
            throw Abort(.notFound, reason: "Employee not found")
        }
        /// Make the object which needs to be added in database
        let profile = ProfileModel(name: createProfileRequest.name ?? "", employeeID: try existingEmployee.requireID())
        /// Add object in the database
        try await profile.create(on: req.db)
        /// Return the response
        return BaseServer(message: "Profile created successfully", status: .ok)
    }
}
