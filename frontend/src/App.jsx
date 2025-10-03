import { Toaster } from "react-hot-toast";
import { Chat } from './component/Chat.jsx'
import { Footer } from "./component/Footer.jsx";
import { Navbar } from "./component/Navbar.jsx";
import { Banner } from "./component/Banner.jsx";
function App() {

  return (
    <>
      <Navbar/>
      <Banner/>
      <Chat/>
      <Footer/>
      <Toaster/>
    </>
  )
}

export default App