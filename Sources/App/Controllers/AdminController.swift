//
//  AdminController.swift
//  Nextlog-server
//
//  Created by Telha Wasim on 18/03/2025.
//

import Vapor
import Fluent
import FluentMongoDriver

struct AdminController: RouteCollection {
    
    //MARK: - BOOT -
    func boot(routes: any RoutesBuilder) throws {
        let admin = routes.grouped("admin")

        admin.post("add", use: self.addAdmin)
        admin.post("login", use: self.loginAsAdmin)
    }
}

//MARK: - FUNCTIONS -
extension AdminController {
    
    //MARK: - ADD ADMIN -
    @Sendable private func addAdmin(req: Request) async throws -> AddAdminResponse {
        /// Decode the request parameters
        let addAdminRequest = try req.content.decode(AddAdminRequest.self)
        /// Validate the request
        try addAdminRequest.validate()
        /// Extract the object where email is already added in database
        let existingAdmin = try await AdminModel.query(on: req.db)
            .filter(\.$email == addAdminRequest.email ?? "")
            .first()
        /// Check if same email exists, we will throw an error
        if (existingAdmin != nil) {
            throw Abort(.badRequest, reason: "Admin with this email already exists")
        }
        /// Encrypt the password
        let hashedPassword = try Bcrypt.hash(addAdminRequest.password ?? "")
        /// Save the provided data in model
        let admin = AdminModel(
            id: ObjectId(),
            email: addAdminRequest.email ?? "",
            password: hashedPassword,
            role: "admin"
        )
        /// Save in the database
        try await admin.save(on: req.db)
        /// Return
        return AddAdminResponse(message: "Success", status: .ok, data: AdminResponseModel(id: admin.id, email: admin.email, role: admin.role))
    }
    
    //MARK: - LOGIN AS ADMIN -
    @Sendable private func loginAsAdmin(req: Request) async throws -> AddAdminResponse {
        /// Decode the request parameters
        let loginAdminRequest = try req.content.decode(AddAdminRequest.self)
        /// Validate the request
        try loginAdminRequest.validate()
        /// Extract the admin from the database
        guard let admin = try await AdminModel.query(on: req.db)
            .filter(\.$email == loginAdminRequest.email ?? "")
            .first() else {
            throw Abort(.notFound, reason: "Admin with this email doesn't exist")
        }
        /// Match the password which is saved in database
        guard try Bcrypt.verify(loginAdminRequest.password ?? "", created: admin.password) else {
            throw Abort(.unauthorized, reason: "Email or password is incorrect")
        }
        
        return AddAdminResponse(message: "Success", status: .ok, data: AdminResponseModel(id: admin.id, email: admin.email, role: admin.role))
    }
}
