import { Composition } from "remotion";
import { HelloWorld } from "./HelloWorld";

export const RemotionRoot: React.FC = () => (
  <Composition
    id="HelloWorld"
    component={HelloWorld}
    durationInFrames={150}
    fps={30}
    width={1080}
    height={1920}
    defaultProps={{ titre: "Annonce prête en 10 secondes" }}
  />
);
