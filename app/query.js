function() {
    var now = new Date();
    var expirationDate = obj._id.getTimestamp();
    expirationDate.setSeconds(
        expirationDate.getSeconds() + obj.expires
    );
    return expirationDate < now;
}