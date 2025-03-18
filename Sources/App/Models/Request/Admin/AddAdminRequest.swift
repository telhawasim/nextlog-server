//
//  AddAdminRequest.swift
//  Nextlog-server
//
//  Created by Telha Wasim on 18/03/2025.
//

import Vapor

struct AddAdminRequest: Content {
    var email: String?
    var password: String?
    
    //MARK: - VALIDATE -
    func validate() throws {
        guard let email = self.email else {
            throw Abort(.badRequest, reason: "Email is required")
        }
        guard let password = self.password else {
            throw Abort(.badRequest, reason: "Password is required")
        }
        if (email.isEmpty) {
            throw Abort(.badRequest, reason: "Email cannot be empty")
        }
        if !(email.isValidEmail()) {
            throw Abort(.badRequest, reason: "Email must be valid")
        }
        if (password.isEmpty) {
            throw Abort(.badRequest, reason: "Password cannot be empty")
        }
    }
}
