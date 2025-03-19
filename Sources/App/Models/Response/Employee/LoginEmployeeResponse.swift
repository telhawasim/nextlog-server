//
//  LoginEmployeeResponse.swift
//  Nextlog-server
//
//  Created by Telha Wasim on 19/03/2025.
//

import Vapor
@preconcurrency import FluentMongoDriver

//MARK: - LoginEmployeeResponse -
struct LoginEmployeeResponse: BaseServerModel {
    var message: String
    var status: HTTPStatus
    var access_token: String?
    var data: LoginEmployee?
}

//MARK: - LoginEmployee -
struct LoginEmployee: Content {
    var id: ObjectId?
    var name: String?
    var role: String?
}
