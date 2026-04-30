class AmityMessageRepository {
    /* begin_public_function
       id: message.delete
       api_style: async
    */
    fun deleteMessage(messageId: String) {}
    /* end_public_function */

    /* begin_public_function
       id: message.flag, message.unflag
    */
    fun flagMessage(messageId: String) {}
    fun unflagMessage(messageId: String) {}
    /* end_public_function */
}
