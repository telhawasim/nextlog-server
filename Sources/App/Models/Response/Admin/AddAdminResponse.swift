//
//  AddAdminResponse.swift
//  Nextlog-server
//
//  Created by Telha Wasim on 18/03/2025.
//

import Vapor
@preconcurrency import FluentMongoDriver

struct AddAdminResponse: BaseServerModel {
    var message: String
    var status: HTTPStatus
    var data: AdminResponseModel?
}

struct AdminResponseModel: Content {
    var id: ObjectId?
    var email: String
    var role: String
}
