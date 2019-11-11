var http = require('http');
var express = require('express');
var fs = require('fs'); // 파일 업로드를 위해 필요
var cors = require('cors');

var app = express();
app.set('views', __dirname + '/views'); //  /views 를 html이 있는 폴더로 설정한다.
app.set('view engine', 'ejs'); // ejs라는 npm 모듈을 view engine으로 사용하겠다.
app.engine('html', require('ejs').renderFile); // ejs라는 npm 모듈을 이용해서 html을 랜더링 할 것이다.

// CORS 설정
app.use(cors());

app.use(express.static(__dirname + '/views')); // 서버파일 위치/views 폴더를 기본 폴더 경로로 설정한다.(ex: /css 이렇게 해도 상대경로를 찾는다.)
app.use(express.static(__dirname)); // 서버파일 위치/views 폴더를 기본 폴더 경로로 설정한다.(ex: /css 이렇게 해도 상대경로를 찾는다.)

app.get('/', function(req, res) {
	res.render('index.html'); // html 파일을 클라이언트에게 랜더링해준다.
});

var server = app.listen(8888, function(){ // express 로 서버 열기
	console.log('['+new Date().toString().substring(4, 24) + '] '+"server startup!");
});