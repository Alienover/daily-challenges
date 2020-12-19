<html>
  <header>
    <style>
      *, *::before, *::after {
        -webkit-box-sizing: border-box;
        box-sizing: border-box;
      }
      pre, code, kbd, samp {
          font-size: 1em;
          font-family: 'SFMono-Regular', Consolas, 'Liberation Mono', Menlo, Courier, monospace;
      }
      pre {
        white-space: pre-wrap;
        color: #333;
        background: #f5f5f5;
        padding: 9.5px;
        border-radius: 15px;
      }
      code {
        padding: 2px 4px;
        font-size: 90%;
        color: #c7254e;
        background-color: #f9f2f4;
        border-radius: 4px;
      }
      .container {
        width: '100%';
        height: '100%';
        background: #fafafa;
        line-height: 24px;
      }
      .title {
        padding: 35px 20px 15px 20px;
        margin: 0;
      }
      .title > a {
        font-size: 14px;
        padding: 0 10px;
      }
      .question-area {
        padding: 20px;
      }
      .question-detail {
        padding: 20px;
        border-radius: 15px;
        background: white;
      }
      .url-container {
        text-align: center;
        padding-bottom: 35px;
      }
      .original-url {
        width: 250px;
        display: block;
        margin: auto;
        padding: 10px;
        background: #136AEE;
        color: white;
        font-weight: bold;
        border-radius: 15px;
        text-align: center;
        text-decoration: none!important;
      }
    </style>
  </header>
  <body>
    <div class="container">
      <h2 class="title">
        $title
        <a class="link" href="$problem_url" target="__blank">
            [Link]
        </a>
      </h2>
      <div class="question-area">
        <div class="question-detail">$content</div>
      </div>
      <div class="url-container">
        <a class="original-url" href="$challenge_url" target="__blank">
            Go and submit your answer
        </a>
      </div>
    </div>
  </body>
</html>
