//
//  JWTMiddleware.swift
//  Nextlog-server
//
//  Created by Telha Wasim on 19/03/2025.
//

import Vapor
import FluentMongoDriver

struct JWTMiddleware: AsyncMiddleware {
    
    func respond(to request: Request, chainingTo next: any AsyncResponder) async throws -> Response {
        guard let token = request.headers.bearerAuthorization?.token else {
            throw Abort(.unauthorized, reason: "Missing or invalid token")
        }
        
        do {
            let payload = try await request.jwt.verify(token, as: JWTTokenPayload.self)
            request.auth.login(payload)
            return try await next.respond(to: request)
        } catch let error as Abort {
            // Show the actual error if it's an Abort error
            throw error
        } catch {
            // If any other unexpected error happens, return generic message
            throw Abort(.unauthorized, reason: "Token verification failed: \(error.localizedDescription)")
        }
    }
}
