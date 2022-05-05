const express = require("express");
const app = express();//app is the instance of the express module.
app.use(express.json())

const fs = require('fs')
var $ = jQuery = require('jquery');
var csv = require('jquery-csv');

const mongo = require("mongodb").MongoClient;//for connecting to mongodb...

const cors = require("cors")
app.use(cors())

app.use(express.static(__dirname + '/'));

const root = __dirname;
var database

const mongourl = "mongodb+srv://technet:awesomeproject@technetmongo.kalqd.mongodb.net/technetmongo?retryWrites=true&w=majority";
//const mongourl = "mongodb://192.168.1.11:27017/technet"



app.get("/", function(req, res){
 console.log(root +"/default.html")
 res.sendFile(root +"/Homepage.html")
 res.status(200)
})

app.get("/Home", function(req, res){
 console.log(root +"/Homepage.html")
 res.sendFile(root +"/Homepage.html")
 res.status(200)
})

app.get("/About", function(req, res){
 console.log(root +"/AboutUs.html")
 res.sendFile(root +"/AboutUs.html")
 res.status(200)
})
app.get("/charts", function(req, res){
 res.sendFile(root +"/finalMongoTableChartAll.html")
 //res.sendFile(root +"/finalMongoTableChart.css")
 //res.sendFile(root +"/webjs1.js")
 
 res.status(200)
})
app.get("/mongotemp1", function(req, res){
	database.collection('temperature1').find({}).toArray((err,result) => {
	if(err) throw err;
	res.send((result));
	})
})

app.get("/mongotemp2", function(req, res){
	database.collection('temperature2').find({}).toArray((err,result) => {
	if(err) throw err;
	res.send((result));
	})
})

app.get("/logcsv", function (req,res){
 var sample = root+'/mycsv.csv';
 fs.readFile(sample,'UTF-8',function(err,result){
	var csvfile=$.csv.toObjects(result);
	res.send(csvfile);
 })
})

app.listen(1234, () => {
console.log("Server is up and running at 1234")
mongo.connect(mongourl,{useNewUrlParser: true}, (err ,result) => {
if(err) throw err;
database = result.db('technet');
console.log('MongoDB connection successful..!')
})
})
