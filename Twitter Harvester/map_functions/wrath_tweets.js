function (doc) {
    if (doc.sentiment_score < -0.5) {
        emit (doc.lga_area, doc.coordinates)
    }
}