import axios from "axios";

class ServerInterface {
  constructor(URL = import.meta.env.VITE_SERVER_URL) {

    if (ServerInterface._instance) {
      return ServerInterface._instance;
    }
    ServerInterface._instance = this;

    this.URL = URL;
    this.axios = axios.create({ baseURL: URL });
  }

  async getTest() {
    return await this.axios.get("/api/test");
  }
}


export { ServerInterface };
