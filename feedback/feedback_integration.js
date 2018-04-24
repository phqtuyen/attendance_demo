/* exported Script */
    /* globals Store */

    class Script {
      prepare_outgoing_request({ request }) {
        let match;

        console.log('lastCmd', Store.get('lastCmd'));

        match = request.data.text.match(/^attendance last$/);
        if (match && Store.get('lastCmd')) {
          request.data.text = Store.get('lastCmd');
        }

        match = request.data.text.match(/^feedback\s(start)\s*(.)*$/);
        
        if (match) {
          Store.set('lastCmd', request.data.text);
          let u = request.url;
          let user_id = request.data.user_id
          let user_name = request.data.user_name
          
          u = u + '&username=' + request.data.user_name + '&role=' + request.data.roles
              + '&name=' + request.data.name + '&email=' + request.data.emails;
          return {
            url: u,
            headers: request.headers,
            method: 'GET'
          };
        }
      }

      process_outgoing_response({ request, response }) {
        var text = ["asd", "asb"];

        return {
          content: {
            text: '',
            parseUrls: false
          }
        };
      }
    }