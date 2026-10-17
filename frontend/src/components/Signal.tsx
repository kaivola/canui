import { Card, Flex, Slider, Switch, Text } from "@radix-ui/themes";
import { type FocusEvent, type KeyboardEvent, memo, useState } from "react";
import type { Signal as SignalType } from "../types/schema";

interface Props {
  signal: SignalType;
  onChange: (signalName: string, value: number) => void;
}

export const Signal = memo(({ signal, onChange }: Props) => {
  const [editMode, setEditMode] = useState<boolean>(false);

  const saveInput = (
    e: FocusEvent<HTMLInputElement> | KeyboardEvent<HTMLInputElement>,
  ) => {
    if ("key" in e && e.key !== "Enter") {
      return;
    }
    const val = Number(e.currentTarget.value);

    onChange(signal.name, val);
    setEditMode(false);
  };

  return (
    <Card mb={"4"}>
      <Flex direction={"column"} gap={"6"}>
        <Flex direction={"column"}>
          <Flex justify={"between"} align={"center"}>
            <Text size={"4"}>{signal.displayName}</Text>
            {editMode ? (
              <input
                id={signal.name}
                defaultValue={signal.value}
                onBlur={saveInput}
                onKeyDown={saveInput}
              />
            ) : (
              <Text onClick={() => setEditMode(true)} size={"7"}>
                {signal.value}
              </Text>
            )}
          </Flex>
          <Text style={{ color: "var(--gray-10)" }}>{signal.comment}</Text>
        </Flex>
        {signal.length > 1 ? (
          <Slider
            value={[signal.value]}
            onValueChange={(e) => onChange(signal.name, e[0])}
            min={signal.nominal_min ?? 0}
            max={signal.nominal_max ?? Number.MAX_SAFE_INTEGER}
            step={signal.step}
          />
        ) : (
          <Switch
            onCheckedChange={(val) => onChange(signal.name, val ? 1 : 0)}
          />
        )}
      </Flex>
    </Card>
  );
});
