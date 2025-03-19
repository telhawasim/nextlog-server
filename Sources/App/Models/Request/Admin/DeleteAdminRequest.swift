//
//  DeleteAdminRequest.swift
//  Nextlog-server
//
//  Created by Telha Wasim on 19/03/2025.
//

import Vapor
@preconcurrency import FluentMongoDriver

struct DeleteAdminRequest: Content {
    var id: ObjectId?
    
    func validate() throws {
        guard let _ = self.id else {
            throw Abort(.badRequest, reason: "ID is required")
        }
    }
}
