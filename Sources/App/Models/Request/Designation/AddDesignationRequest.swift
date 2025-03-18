//
//  AddDesignationRequest.swift
//  Nextlog-server
//
//  Created by Telha Wasim on 18/03/2025.
//

import Vapor

struct AddDesignationRequest: Content {
    var name: String?
    
    //MARK: - VALIDATE -
    func validate() throws {
        guard let name = self.name else {
            throw Abort(.badRequest, reason: "Name is required")
        }
        
        if (name == "") {
            throw Abort(.badRequest, reason: "Name cannt be empty")
        }
    }
}
