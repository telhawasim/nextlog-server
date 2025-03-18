//
//  DeleteEmployeeRequest.swift
//  Nextlog-server
//
//  Created by Telha Wasim on 18/03/2025.
//

import Foundation
import Vapor
@preconcurrency import FluentMongoDriver

struct DeleteEmployeeRequest: Content {
    var id: ObjectId?
    
    //MARK: - VALIDATE -
    func validate() throws {
        if (self.id == nil) {
            throw Abort(.badRequest, reason: "ID is required")
        }
    }
}
