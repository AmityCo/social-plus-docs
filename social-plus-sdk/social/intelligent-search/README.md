# Intelligent Search

## Intelligent Search

Enhancing content discovery with an intuitive approach, allowing users to explore content based on context rather than just keywords. With the `semanticSearchPosts()` and `semanticSearchcommunities()` functions, the Amity SDK provides a LiveCollection of search results that prioritize relevance to the user. By utilizing advanced context recognition, semantic search enriches the discovery experience, helping users find content and communities they might not have initially been aware of, thereby boosting community engagement.

## Enable the Feature

To use this feature, please get in touch with our [support](mailto:support.asc@amity.co) directly.

## API Parameters

You can access this feature through the SDK or by making direct [HTTP API](https://api-docs.amity.co/#/Semantic%20Search/get_api_v1_semantic_search_posts) calls. Below is an explanation of the function parameters:

#### Search Term

* `query`: The search term. You can enter words, phrases, or sentences.

#### Supported Languages

The API supports searching in more than 100 languages.

<details>

<summary>Supported Languages</summary>

* Afrikaans
* Albanian
* Amharic
* Arabic
* Armenian
* Assamese
* Azerbaijani
* Bashkir
* Basque
* Belarusian
* Bengali
* Bosnian
* Breton
* Bulgarian
* Burmese
* Catalan
* Cebuano
* Chinese
* Corsican
* Croatian
* Czech
* Danish
* Dhivehi
* Dutch
* English
* Esperanto
* Estonian
* Faroese
* Finnish
* French
* Galician
* Georgian
* German
* Greek (Modern)
* Gujarati
* Haitian
* Hausa
* Hebrew
* Hindi
* Hungarian
* Icelandic
* Indonesian
* Irish
* Italian
* Japanese
* Javanese
* Kannada
* Kazakh
* Khmer
* Kirghiz
* Kinyarwanda
* Korean
* Kurdish
* Lao
* Latin
* Latvian
* Lithuanian
* Luxembourgish
* Malagasy
* Malay
* Malayalam
* Maltese
* Marathi
* Maori
* Mongolian
* Nepali
* Norwegian
* Norwegian Nynorsk
* Occitan
* Oriya
* Punjabi
* Pashto
* Persian
* Polish
* Portuguese
* Romanian
* Russian
* Sanskrit
* Serbian
* Sindhi
* Sinhala
* Slovak
* Slovenian
* Somali
* Spanish
* Sundanese
* Swahili
* Swedish
* Tagalog
* Tajik
* Tamil
* Tatar
* Telugu
* Thai
* Tibetan
* Turkish
* Turkmen
* Ukrainian
* Urdu
* Uzbek
* Vietnamese
* Welsh
* Western Frisian
* Xhosa
* Yiddish
* Yoruba
* Zulu

</details>

## Search Result Score <a href="#search-result-score" id="search-result-score"></a>

This API returns a score for each item, ranging from 0 to 1. The score is calculated based on two factors—lexical and semantic—that are weighted differently.

* **Lexical score**: contributes 30% of the total score. If a post, community name, or description contains text that matches the search term, it will be assigned a higher lexical score.
* **Semantic score**: contributes 70% of the total score. The more relevant a post or community is to the meaning of the search term, the higher its semantic score will be.

### Filtering Results by Minimum Score <a href="#filtering-results-by-minimum-score" id="filtering-results-by-minimum-score"></a>

All matched items are included by default, even with a low score. However, you can adjust the minimum score filter based on the content and your specific use case. Any item with a score lower than the specified threshold will be excluded from the results.

#### **Example search query - "Red Fruits"** <a href="#example-search-query-red-fruits" id="example-search-query-red-fruits"></a>

* **Low Threshold**: This shows various fruits, even those loosely related to the search term. For example, results could include apples, strawberries, and even unrelated fruits like bananas (not red).&#x20;
* **High Threshold**: This filters results to show only highly relevant matches, such as cherries and raspberries while excluding unrelated fruits like bananas or green apples.

The API is available at [Network Settings - Semantic Search](https://api-docs.amity.co/#/Network%20Setting/put_api_v3_network_settings_semantic_search) (requires admin permission).

### Limitations <a href="#limitations" id="limitations"></a>

* Recent user activity is not considered when determining the relevance of search results.&#x20;
* Real-time search suggestions while typing are not supported across all APIs.
