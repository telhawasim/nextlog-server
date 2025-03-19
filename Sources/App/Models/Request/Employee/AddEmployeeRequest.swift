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
    var emp_id: Int?
    var avatar: File?
    var dob: Date?
    var phone: String?
    var date_of_joining: Date?
    var designation_id: ObjectId?
    var department_id: ObjectId?
    
    //MARK: - VALIDATE -
    func validate() throws {
        guard let name = self.name else {
            throw Abort(.badRequest, reason: "Name is required")
        }
        guard let email = self.email else {
            throw Abort(.badRequest, reason: "Email is required")
        }
        guard let _ = self.emp_id else {
            throw Abort(.badRequest, reason: "Employee ID is required")
        }
        guard let avatar = self.avatar else {
            throw Abort(.badRequest, reason: "Profile picture is required")
        }
        guard let _ = self.designation_id else {
            throw Abort(.badRequest, reason: "Designation ID is required")
        }
        guard let _ = self.department_id else {
            throw Abort(.badRequest, reason: "Department ID is required")
        }
        guard let _ = self.dob else {
            throw Abort(.badRequest, reason: "Date of Birth is required")
        }
        guard let phone = self.phone else {
            throw Abort(.badRequest, reason: "Phone number is required")
        }
        guard let _ = self.date_of_joining else {
            throw Abort(.badRequest, reason: "Date of Joining is required")
        }
        
        if (name == "") {
            throw Abort(.badRequest, reason: "Name cannot be empty")
        } else if (email == "") {
            throw Abort(.badRequest, reason: "Email cannot be empty")
        } else if !(email.isValidEmail()) {
            throw Abort(.badRequest, reason: "Email must be valid")
        } else if (phone == "") {
            throw Abort(.badRequest, reason: "Phone number cannot be empty")
        } else if (avatar.filename == "") {
            throw Abort(.badRequest, reason: "Profile picture cannot be empty")
        }
    }
}
