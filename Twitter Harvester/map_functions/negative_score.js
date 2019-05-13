function (doc) {
    if (doc.sentiment_score < -0.05) {
        emit (doc.lga_area, doc.coordinates)
    }
}