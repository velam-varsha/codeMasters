import React, { Suspense, useState } from "react";
import { BrowserRouter as Router, Route, Routes } from "react-router-dom";
import Sidebar from "./components/Navbars/Sidebar/Sidebar";
// import HomePage from "./components/pages/HomePage";
import HomePage from "./pages/HomePage";
import SignIn from "./pages/SignIn";
import ProfilePage from "./pages/ProfilePage";
import RegisterPage from "./pages/RegisterPage";

import Explore from "./pages/Explore";
import NotFound from "./pages/NotFound";
import NFTPage from "./pages/NFTPage";

function App() {
  // const [Sidebar, setsidebar] = useState(true);
  const [sidebar, setsidebar] = useState(false);

  return (
    <>
      <Router>
        {/* {sidebar === true ? <Sidebar /> : null} */}
        <Sidebar render={sidebar}/>

        <Suspense>
          <Routes>
            {/* uncomment once done completely  */}
            {/* <Route
              path="/"
              element={<PreLoaderPage shouldit={setsidebar} />}
            /> */}

            <Route path="/" element={<HomePage  Sidebarrender={setsidebar}/>} />

            <Route
              path="/SignUp"
              element={<RegisterPage Sidebarrender={setsidebar} />}
            />
            
            {/* <Route path="/donation" element={<About />} /> */}
            <Route
              path="/Signin"
              element={<SignIn Sidebarrender={setsidebar} />}
            />
            <Route
              path="/profile/:id"
              element={<ProfilePage Sidebarrender={setsidebar} />}
            />
            <Route
              path="/explore"
              element={<Explore Sidebarrender={setsidebar} />}
            />
            <Route 
              path="/nft" 
              element={<NFTPage Sidebarrender={setsidebar}/> }
            />
          
            <Route path="*" element={<NotFound />} />
          </Routes>

          {/* <Loader  loader={loader}/> */}
          {/* <Footer /> */}
        </Suspense>
      </Router>
    </>
  );
}

export default App;
