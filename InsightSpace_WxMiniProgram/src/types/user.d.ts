export type LoginResult = {
  username: string
  avatar: string
  id: number
  phone: BigInteger
}
export type ProfileDetail = {
  username: string;
  phone: number;
  is_admin: boolean;
  is_banned: boolean;
  reports: number;
  gender: string,
  grade: string,
  department: string,
}