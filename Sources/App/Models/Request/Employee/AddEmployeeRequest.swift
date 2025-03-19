//
//  AddEmployeeRequest.swift
//  Nextlog-server
//
//  Created by Telha Wasim on 18/03/2025.
//

import Vapor
@preconcurrency import FluentMongoDriver

struct AddEmployeeRequest: Content {
    var name: String?
    var email: String?
    var avatar: File?
    var designation_id: ObjectId?
    var department_id: ObjectId?
    
    func validate() throws {
        guard let name = self.name else {
            throw Abort(.badRequest, reason: "Name is required")
        }
        guard let email = self.email else {
            throw Abort(.badRequest, reason: "Email is required")
        }
        guard let avatar = self.avatar else {
            throw Abort(.badRequest, reason: "Profile picture is required")
        }
        guard let designationID = self.designation_id else {
            throw Abort(.badRequest, reason: "Designation ID is required")
        }
        guard let departmentID = self.department_id else {
            throw Abort(.badRequest, reason: "Department ID is required")
        }
        
        if (name == "") {
            throw Abort(.badRequest, reason: "Name cannot be empty")
        } else if (email == "") {
            throw Abort(.badRequest, reason: "Email cannot be empty")
        } else if !(email.isValidEmail()) {
            throw Abort(.badRequest, reason: "Email must be valid")
        } else if (avatar.filename == "") {
            throw Abort(.badRequest, reason: "Profile picture cannot be empty")
        }
    }
}
