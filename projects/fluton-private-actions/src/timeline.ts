import film from './film-data.json';
export {film};
export type FilmScene=(typeof film.scenes)[number];
export function getSceneAtFrame(frame:number):FilmScene {
 return film.scenes.find(s=>frame>=s.startFrame&&frame<s.endFrameExclusive)??(frame<0?film.scenes[0]:film.scenes[film.scenes.length-1]);
}
