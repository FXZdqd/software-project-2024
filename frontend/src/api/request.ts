import myAxios from "@/api/myAxios";

export const log_in = (username:string,password:string,is_admin:boolean)=> {
  let params = {
    username: username,
    password: password,
    is_admin: is_admin,
  }
  return myAxios.post('/api/login', params, {
    headers: { 'Content-Type': 'application/json'}
  })
}

export const getAllQuestions = ()=> {
  return myAxios.post('/api/getAllQuestion')
}


export const delQuestion = (q_id:number)=> {
  let params = {
    q_id: q_id
  }
  return myAxios.post('/api/delQuestion', params, {
    headers: { 'Content-Type': 'application/json'}
  })
}
