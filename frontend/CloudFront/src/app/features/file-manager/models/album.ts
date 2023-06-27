import {Subalbum} from "./subalbum";
import {File} from "./file";

export interface Album {
  subalbums: Subalbum[];
  files: File[];
}
