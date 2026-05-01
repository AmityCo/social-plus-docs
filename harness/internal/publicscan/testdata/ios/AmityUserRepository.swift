import Foundation

public class AmityUserRepository {

    public func getUser(userId: String) -> String {
        return userId
    }

    public func searchUsers(query: String) -> [String] {
        return []
    }

    open func fetchUserProfile(userId: String) -> String {
        return userId
    }

    func internalHelper() -> Bool {
        return true
    }

    private func privateMethod() -> Void {}
}
