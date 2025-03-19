//
//  LoginEmployeeRequest.swift
//  Nextlog-server
//
//  Created by Telha Wasim on 19/03/2025.
//

import Vapor

struct LoginEmployeeRequest: Content {
    var email: String?
    var emp_id: Int?
    
    //MARK: - VALIDATE -
    func validate() throws {
        guard let email = self.email else {
            throw Abort(.badRequest, reason: "Email is required")
        }
        guard let _ = self.emp_id else {
            throw Abort(.badRequest, reason: "Employee ID is required")
        }
        
        if (email == "") {
            throw Abort(.badRequest, reason: "Email cannot be empty")
        } else if !(email.isValidEmail()) {
            throw Abort(.badRequest, reason: "Email must be valid")
        }
    }
}
