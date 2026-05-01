package com.amity.socialcloud.sdk.api.community

class AmityCommunityRepository(private val client: Any) {

    fun createCommunity(displayName: String): String {
        return displayName
    }

    suspend fun getCommunity(communityId: String): String {
        return communityId
    }

    open fun searchCommunities(query: String): List<String> {
        return emptyList()
    }

    private fun internalHelper(): Boolean {
        return true
    }

    internal fun internalMethod(): Unit {}

    protected fun protectedMethod(): String = ""
}
