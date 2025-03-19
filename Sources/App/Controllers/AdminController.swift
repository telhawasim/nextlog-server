//
//  AdminController.swift
//  Nextlog-server
//
//  Created by Telha Wasim on 18/03/2025.
//

import Vapor
import Fluent
@preconcurrency import FluentMongoDriver
import JWT

struct AdminController: RouteCollection {
    
    //MARK: - BOOT -
    func boot(routes: any RoutesBuilder) throws {
        let admin = routes.grouped("admin")

        admin.post("add", use: self.addAdmin)
        admin.post("login", use: self.loginAsAdmin)
        admin.delete("delete", use: self.deleteAdmin)
        admin.get("getAll", use: self.getAllAdmins)
    }
}

//MARK: - FUNCTIONS -
extension AdminController {
    
    //MARK: - ADD ADMIN -
    @Sendable private func addAdmin(req: Request) async throws -> BaseServer {
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
        return BaseServer(message: "Admin has been added successfully", status: .ok)
    }
    
    //MARK: - LOGIN AS ADMIN -
    @Sendable private func loginAsAdmin(req: Request) async throws -> LoginAdminResponse {
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
        /// Generate JWT Token
        let payload = JWTTokenPayload(
            id: admin.id ?? ObjectId(),
            isAdmin: true,
            exp: ExpirationClaim(value: Date().addingTimeInterval(3600)) // 1 hour
        )
        /// Token into string
        let token = try await req.jwt.sign(payload)
        /// Return required response
        return LoginAdminResponse(
            message: "Success",
            status: .ok,
            access_token: token,
            data: AdminResponseModel(id: admin.id, email: admin.email, role: admin.role)
        )
    }
    
    //MARK: - DELETE ADMIN -
    @Sendable private func deleteAdmin(req: Request) async throws -> BaseServer {
        /// Decode the request parameters
        let deleteAdminRequest = try req.content.decode(DeleteAdminRequest.self)
        /// Validate the request
        try deleteAdminRequest.validate()
        /// Extract the existing Admin
        guard let existingAdmin = try await AdminModel.query(on: req.db)
            .filter(\.$id == deleteAdminRequest.id ?? ObjectId())
            .first()
        else {
            throw Abort(.notFound, reason: "Admin not found")
        }
        /// Delete the admin from the database
        try await existingAdmin.delete(on: req.db)
        /// Return the response
        return BaseServer(message: "Successfully deleted", status: .ok)
    }
    
    //MARK: - GET ALL ADMINS -
    @Sendable private func getAllAdmins(req: Request) async throws -> GetAllAdminResponse {
        /// Extracts all the admins
        let admins = try await AdminModel.query(on: req.db)
            .all()
            .map { admin in
                return AdminResponseModel(id: admin.id, email: admin.email, role: admin.role)
            }
        
        return GetAllAdminResponse(message: "Success", status: .ok, admins: admins)
    }
}
