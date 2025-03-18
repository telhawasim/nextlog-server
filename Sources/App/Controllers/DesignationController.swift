//
//  DesignationController.swift
//  Nextlog-server
//
//  Created by Telha Wasim on 18/03/2025.
//

import Vapor
import Fluent
import FluentMongoDriver

struct DesignationController: RouteCollection {
    
    //MARK: - BOOT -
    func boot(routes: any RoutesBuilder) throws {
        let designation = routes.grouped("designation")

        designation.post("add", use: self.addDesignation)
        designation.get("getAll", use: self.getAllDesginations)
    }
}

//MARK: - FUNCTIONS -
extension DesignationController {
    
    //MARK: - ADD DESIGNATION -
    @Sendable private func addDesignation(req: Request) async throws -> BaseServer {
        /// Decode the request parameters
        let addDesignationRequest = try req.content.decode(AddDesignationRequest.self)
        /// Validate the request
        try addDesignationRequest.validate()
        /// Extract the object where desigantion is already exst in database
        let existingDesignation = try await DesignationModel.query(on: req.db)
            .filter(\.$name == addDesignationRequest.name ?? "")
            .first()
        /// Check if designation already exists
        if (existingDesignation != nil) {
            throw Abort(.badRequest, reason: "Desigantion already exist")
        }
        /// Make an object which needs to be saved in database
        let designation = DesignationModel(
            id: ObjectId(),
            name: addDesignationRequest.name ?? ""
        )
        /// Save in the database
        try await designation.save(on: req.db)
        /// Return
        return BaseServer(message: "Designation added successfully", status: .ok)
    }
    
    //MARK: - GET ALL DESIGNATIONS -
    @Sendable private func getAllDesginations(req: Request) async throws -> GetAllDesignatonsResponse {
        /// Extract the designations from the database
        let designations = try await DesignationModel.query(on: req.db)
            .all()
        /// Return
        return GetAllDesignatonsResponse(message: "Success", status: .ok, designations: designations)
    }
}
