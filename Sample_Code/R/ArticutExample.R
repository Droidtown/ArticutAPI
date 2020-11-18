library(httr)
library(jsonlite)

articutAPIurl <- "https://api.droidtown.co/Articut/API/"
headers <- c('Accept'='application/json', 'Content-Type'='application/json')

payload <- jsonlite::toJSON(list(username="<Your_username_email>",
                                 api_key="<Your_API_Key>",
                                 input_str="我也想過過過兒過過的日子"), 
                            auto_unbox=TRUE)
result <- POST(articutAPIurl, body=payload, add_headers(.headers=headers))

jsonlite::toJSON(content(result))