import {UserRole} from "../constants/user-role";

export interface User {
  id: string;
  email: string;
  role: UserRole;
  token: string;
}
