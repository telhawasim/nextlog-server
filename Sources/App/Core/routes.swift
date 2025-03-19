import Vapor

func routes(_ app: Application) throws {
    try app.register(collection: AdminController())
    try app.register(collection: DesignationController())
    try app.register(collection: DepartmentController())
    try app.register(collection: EmployeeController())
    try app.register(collection: ProfileController())
}
