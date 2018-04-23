/* exported Script */
    /* globals Store */
    extractQuestion = function(str) {
      str = str.replace(/^feedback\s(start)\s/g,'');
      return str;
    }

    class Script {
      prepare_outgoing_request({ request }) {
        let match;

        console.log('lastCmd', Store.get('lastCmd'));

        match = request.data.text.match(/^attendance last$/);
        if (match && Store.get('lastCmd')) {
          request.data.text = Store.get('lastCmd');
        }

        match = request.data.text.match(/^feedback\s(start)\s*(.)*$/);
        
        console.log('lastCmd2', request.data.text);
        console.log('data obj:', request.data);
        console.log('question: ', extractQuestion(request.data.text));
        if (match) {
          Store.set('lastCmd', request.data.text);
          let u = request.url;
          let user_id = request.data.user_id
          let user_name = request.data.user_name
          
          console.log('URL to be sent:', u);
    //attach parameters
          u = u + '&username=' + request.data.user_name + '&role=' + request.data.roles
              + '&name=' + request.data.name + '&email=' + request.data.emails
              + '&question=' + extractQuestion(request.data.text).trim();
          console.log("finish prepare process outgoing request.");
          return {
            url: u,
            headers: request.headers,
            method: 'GET'
          };
        }
      }

      process_outgoing_response({ request, response }) {
        var text = ["asd", "asb"];
        console.log('response', response.content.text);
//        response.content.forEach(function(pr) {
//          text.push('Response for each text');
//          text.push('> '+pr.state+' [#'+pr.number+']('+pr.html_url+') - '+pr.title);
//        });

        return {
          content: {
            text: response.content.text,
            parseUrls: false
          }
        };
      }
    }