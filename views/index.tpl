<!DOCTYPE html>
<html lang="jp">
  <head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <title>HexDump</title>
    <link href="/views/css/bootstrap.min.css" rel="stylesheet">
    <script>
  	  (function(i,s,o,g,r,a,m){i['GoogleAnalyticsObject']=r;i[r]=i[r]||function(){
  	  (i[r].q=i[r].q||[]).push(arguments)},i[r].l=1*new Date();a=s.createElement(o),
  	  m=s.getElementsByTagName(o)[0];a.async=1;a.src=g;m.parentNode.insertBefore(a,m)
  	  })(window,document,'script','//www.google-analytics.com/analytics.js','ga');
  	  ga('create', 'UA-42950958-2', 'shuffleee.com');
  	  ga('send', 'pageview');
  	</script>
  </head>
  <body>
    <nav class="navbar navbar-inverse navbar-fixed-top">
      <div class="container">
        <div class="navbar-header">
          <button type="button" class="navbar-toggle collapsed" data-toggle="collapse" data-target="#navbar" aria-expanded="false" aria-controls="navbar">
            <span class="sr-only">Toggle navigation</span>
            <span class="icon-bar"></span>
            <span class="icon-bar"></span>
            <span class="icon-bar"></span>
          </button>
          <a class="navbar-brand" href="#">Project name</a>
        </div>
        <div id="navbar" class="collapse navbar-collapse">
          <ul class="nav navbar-nav">
            <li class="active"><a href="#">Home</a></li>
            <li><a href="#usage">Usage</a></li>
            <li><a href="#contact">Contact</a></li><!-- 未定 -->
          </ul>
        </div>
      </div>
    </nav>
    <br />
    <br />
    <div class="container">

      <div class="starter-template">
        <h1>Bootstrap starter template</h1>
        <p class="lead">Use this document as a way to quickly start any new project.<br> All you get is this text and a mostly barebones HTML document.</p>

        <form enctype="multipart/form-data" action="" name="form" method="post">
  		<br>
  		<input type="file" id="file_input" name="file_input" style="display: none;">
  		<div style="width:40%;float:left;margin-right:10px;" class="input-group">
  			<span class="input-group-btn">
  				<button class="btn btn-default" type="button" onclick="$('#file_input').click();"><i class="glyphicon glyphicon-folder-open"></i></button>
  			</span>
  			<input id="dummy_file" type="text" class="form-control" placeholder="select file..." disabled>
  		</div>
  		<input type="submit" name="csv_up" class="btn btn-primary" value="upload">
  	</form>
  	<script src="https://ajax.googleapis.com/ajax/libs/jquery/1.9.1/jquery.min.js"></script><!-- jquery 本体-->
  	<script src="https://ajax.googleapis.com/ajax/libs/jqueryui/1.10.3/jquery-ui.min.js"></script><!-- jquery-UI 本体-->
  	<script src="//netdna.bootstrapcdn.com/bootstrap/3.0.0/js/bootstrap.min.js"></script>
  	<script type="text/javascript">
  	$(function(){
  		$('#file_input').change(function() {
  			$('#dummy_file').val($(this).val());
  		});
  	})
    </script>
      </div>

    </div><!-- /.container -->
    <script src="/viewsjs/bootstrap.min.js"></script>
  </body>
