//
//  BaseServerModel.swift
//  Nextlog-server
//
//  Created by Telha Wasim on 18/03/2025.
//

import Vapor

protocol BaseServerModel: Content {
    var message: String { get }
    var status: HTTPStatus { get }
}
