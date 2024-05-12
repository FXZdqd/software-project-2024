export type LoginResult = {
  username: string
  avatar: string
  id: number
  phone: BigInteger
}
export type ProfileDetail = {
  user_id: number;
  username: string;
  phone: number;
  is_admin: boolean;
  is_baned: boolean;
}