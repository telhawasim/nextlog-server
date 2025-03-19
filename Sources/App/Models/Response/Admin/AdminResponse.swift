//
//  AdminResponse.swift
//  Nextlog-server
//
//  Created by Telha Wasim on 19/03/2025.
//

import Vapor
@preconcurrency import FluentMongoDriver

struct AdminResponseModel: Content {
    var id: ObjectId?
    var email: String
    var role: String
}
