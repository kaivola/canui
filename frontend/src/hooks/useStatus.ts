import { useEffect, useState } from "react";
import { BACKEND_URL } from "../utils/constants";

export const useStatus = () => {
  const [isTransmitting, setIsTransmitting] = useState(false);

  const changeStatus = (status: "start" | "stop") => {
    fetch(BACKEND_URL + "/status", {
      method: "put",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({ status }),
    })
      .then((res) => res.json())
      .then((json) => setIsTransmitting(json.isBroadcasting))
      .catch((e) => console.error(e));
  };

  useEffect(() => {
    fetch(BACKEND_URL + "/status")
      .then((res) => {
        return res.json();
      })
      .then((json) => {
        setIsTransmitting(json.isBroadcasting);
      })
      .catch((e) => console.error(e));
  }, []);

  return { isTransmitting, changeStatus };
};
