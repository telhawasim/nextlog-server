//
//  AddEmployeeResquest.swift
//  Nextlog-server
//
//  Created by Telha Wasim on 18/03/2025.
//

import Vapor

struct AddEmployeeResquest: Content {
    var name: String
    var email: String
    var avatar: File
}
