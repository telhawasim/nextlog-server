//
//  LoginAdminResponse.swift
//  Nextlog-server
//
//  Created by Telha Wasim on 19/03/2025.
//

import Vapor

struct LoginAdminResponse: BaseServerModel {
    var message: String
    var status: HTTPStatus
    var access_token: String?
    var data: AdminResponseModel?
}
