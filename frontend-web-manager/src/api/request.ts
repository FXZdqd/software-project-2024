import myAxios from "@/api/myAxios";

export const log_in = (
  username: string,
  password: string,
  is_admin: boolean
) => {
  let params = {
    username: username,
    password: password,
    is_admin: is_admin,
  };
  return myAxios.post("/api/login", params, {
    headers: { "Content-Type": "application/json" },
  });
};

export const getAllQuesByReport = () => {
  return myAxios.post("/api/getAllQuestionByReport");
};
export const getAllUserByReport = () => {
  return myAxios.post("/api/getAllUserByReport");
};

export const delQuestion = (q_id: number) => {
  let params = {
    q_id: q_id,
  };
  return myAxios.post("/api/delQuestion", params, {
    headers: { "Content-Type": "application/json" },
  });
};
export const banUser = (username: string) => {
  let params = {
    username: username,
  };
  return myAxios.post("/api/banUser", params, {
    headers: { "Content-Type": "application/json" },
  });
};
export const searchUser = (username: string) => {
  let params = {
    keyword: username,
  };
  return myAxios.post("/api/searchUser", params, {
    headers: { "Content-Type": "application/json" },
  });
};
export const GetQuesByKeyword = (keyword: string) => {
  let params = {
    keyword: keyword,
  };
  return myAxios.post("/api/getQuestionByKeyword", params, {
    headers: { "Content-Type": "application/json" },
  });
};
export const GetQuesByTag = (tag_name: string) => {
  let params = {
    tag_name: tag_name,
  };
  return myAxios.post("/api/getQuestionByTag", params, {
    headers: { "Content-Type": "application/json" },
  });
};
