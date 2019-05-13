function (doc) {
    if (doc.sentiment_score < -0.05) {
        emit ('negative', 1)
    } else if (doc.sentiment_score > 0.05) {
        emit ('positive', 1)
    } else {
        emit ('neutral', 1)
    }
}