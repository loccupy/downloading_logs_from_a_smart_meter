#
#  --------------------------------------------------------------------------
#   Gurux Ltd
#
#
#
#  Filename: $HeadURL$
#
#  Version: $Revision$,
#                   $Date$
#                   $Author$
#
#  Copyright (c) Gurux Ltd
#
# ---------------------------------------------------------------------------
#
#   DESCRIPTION
#
#  This file is a part of Gurux Device Framework.
#
#  Gurux Device Framework is Open Source software; you can redistribute it
#  and/or modify it under the terms of the GNU General Public License
#  as published by the Free Software Foundation; version 2 of the License.
#  Gurux Device Framework is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
#  See the GNU General Public License for more details.
#
#  More information of Gurux products: http://www.gurux.org
#
#  This code is licensed under the GNU General Public License v2.
#  Full text may be retrieved at http://www.gnu.org/licenses/gpl-2.0.txt
# ---------------------------------------------------------------------------
#pylint: disable=broad-except,no-name-in-module
try:
    from enum import IntEnum
    __base = IntEnum
except Exception:
    __base = object

class Parity(__base):
    """Specifies the parity bit for a System.IO.Ports.SerialPort object."""
    NONE = 0
    """No parity check occurs."""
    ODD = 1
    """Sets the parity bit so that the count of bits set is an odd number."""
    EVEN = 2
    """Sets the parity bit so that the count of bits set is an even number."""
    MARK = 3
    """Leaves the parity bit set to 1."""
    SPACE = 4
    """Leaves the parity bit set to 0."""
