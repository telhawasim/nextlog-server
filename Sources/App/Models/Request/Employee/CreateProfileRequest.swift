//
//  CreateProfileRequest.swift
//  Nextlog-server
//
//  Created by Telha Wasim on 19/03/2025.
//

import Vapor
@preconcurrency import FluentMongoDriver

struct CreateProfileRequest: Content {
    var employee_id: ObjectId?
    var name: String?
    
    //MARK: - VALIDATE -
    func validate() throws {
        guard let _ = self.employee_id else {
            throw Abort(.badRequest, reason: "Employee ID is required")
        }
        guard let _ = self.name else {
            throw Abort(.badRequest, reason: "Name is required")
        }
    }
}
