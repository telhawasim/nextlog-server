//
//  GetProfileResponse.swift
//  Nextlog-server
//
//  Created by Telha Wasim on 19/03/2025.
//

import Vapor
@preconcurrency import FluentMongoDriver

struct GetProfileResponse: Content {
    var id: ObjectId?
    var name: String?
}
