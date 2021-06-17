var MongoClient = require('mongodb').MongoClient;
const uri = "mongodb+srv://dbUser:yourDBname@yourMongodb/yourDatabase?retryWrites=true&w=majority"
// Connect to the db
const client = new MongoClient(uri, { useNewUrlParser: true, useUnifiedTopology: true });
client.connect(err => {
    console.log('mongodb is running!'); 
        client.close();
})

exports.insertOne = function(data) {
    MongoClient.connect(uri, function(err, db) {
        if (err) throw err;
        var dbo = db.db("outputData");
        dbo.collection("faceCollection").insertOne(data, function(err, res) {
          if (err) throw err;
          console.log("1 document inserted");
          db.close();
        });
    });
}


exports.insertOneAsync = function(data) {
    return new Promise(function (resolve, reject) {
      MongoClient.connect(uri, function(err, db) {
        if (err) throw err;
        var dbo = db.db("outputData");
        dbo.collection("faceCollection").insertOne(data, function(err, res) {
          if (err) {
            reject(err);
            throw err;
          }
          console.log("1 document inserted");
          resolve(res);
          db.close();
        });
    });
    });
}

exports.findAsync = function(data) {
    return new Promise(function (resolve, reject) {
    MongoClient.connect(uri, function(err, db) {
        if (err) throw err;
        var dbo = db.db("outputData");
        dbo.collection("faceCollection").find({}).toArray(function (err, result) {
            if (err) {
                reject(err);
            }
            // console.log(result);
            resolve(result);
            client.close();
        });
    });
    });
}