import { AbsoluteFill, interpolate, spring, useCurrentFrame, useVideoConfig } from "remotion";

export const HelloWorld: React.FC<{ titre: string }> = ({ titre }) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  const scale = spring({ frame, fps, config: { damping: 12 } });
  const opacity = interpolate(frame, [0, 20], [0, 1], { extrapolateRight: "clamp" });

  return (
    <AbsoluteFill style={{ backgroundColor: "#0f172a", justifyContent: "center", alignItems: "center" }}>
      <h1 style={{ color: "white", fontSize: 90, fontFamily: "sans-serif", textAlign: "center", padding: 60, transform: `scale(${scale})`, opacity }}>
        {titre}
      </h1>
    </AbsoluteFill>
  );
};
