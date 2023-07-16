import React, { useEffect, useState } from "react";
import { getallposts } from "../../api/allpost";
import ExploreCard from "../posts/ExploreCard";
import { getExplorePosts } from "../../api/explore";

const ExploreTable = (props) => {
  const [exploredata, setexploredata] = useState([]);

  useEffect(() => {
    renderexplore();
  }, []);

  const renderexplore = async () => {
    const { data } = await getExplorePosts();
    setexploredata(data);
    console.log(exploredata);
  };

  // placehlder for getposts
  // let user_id = 29;
  // useEffect(() => {
  //   load();
  // }, []);
  // const load = async () => {
  //   let data = await getallposts(user_id);
  //   data = await data.data;
  //   console.log("data:", data);
  //   setexploredata(data);
  // };

  return (
    <div className="bg-white w-full">
      <div className="flex flex-row m-auto mt-[8vh] w-10/12 ">
        <div className="w-1/3">
          {exploredata !== []
            ? exploredata?.map((element, index) => {
                if (index % 3 == 0) {
                  return (
                    <div key={element}>
                      <ExploreCard element={element} />
                    </div>
                  );
                }
              })
            : null}
        </div>
        <div className="w-1/3">
          {exploredata !== []
            ? exploredata?.map((element, index) => {
                if (index % 3 == 1) {
                  return (
                    <div key={element}>
                      <ExploreCard element={element} />
                    </div>
                  );
                }
              })
            : null}
        </div>
        <div className="w-1/3">
          {exploredata !== []
            ? exploredata?.map((element, index) => {
                if (index % 3 == 2) {
                  return (
                    <div key={element}>
                      <ExploreCard element={element} />
                    </div>
                  );
                }
              })
            : null}
        </div>
      </div>
    </div>
  );
};

export default ExploreTable;
